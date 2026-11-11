#!/usr/bin/env python3
"""Synthetic-only teaching demo: planar UWB range + measured-IMU EKF.

The true trajectory, all sensor readings, and every output are artificial.
The filter never reads ground truth: ground truth is used only to generate
measurements and for offline scoring/plotting after the run.
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import time
from pathlib import Path

import numpy as np

LABEL = "SYNTHETIC_TEACHING_ONLY"
SEED = 20261111
DT = 0.1
DURATION = 60.0
RANGE_PERIOD = 0.5
RADIUS = 8.0
OMEGA = 0.11
CENTER = np.array([0.0, 0.0], dtype=float)
ANCHORS = np.array(
    [
        [-12.0, -9.0],
        [13.0, -8.0],
        [12.0, 12.0],
        [-11.0, 13.0],
    ],
    dtype=float,
)
NOMINAL_STATE = np.array(
    [CENTER[0] + RADIUS, CENTER[1], 0.0, RADIUS * OMEGA], dtype=float
)
INITIAL_PERTURBATION = np.array([0.18, -0.12, 0.02, -0.03], dtype=float)
INITIAL_COV = np.diag([0.35**2, 0.35**2, 0.10**2, 0.10**2])
ACCEL_SIGMA = 0.10
YAW_SIGMA = 0.02
RANGE_SIGMA = 0.18
PROCESS_ACCEL_SIGMA = 0.12
RANGE_SINGULAR_TOL = 1e-9


def wrap_angle(angle):
    """Wrap an angle to [-pi, pi)."""
    return (angle + math.pi) % (2.0 * math.pi) - math.pi


def rotation_matrix(angle):
    c = math.cos(angle)
    s = math.sin(angle)
    return np.array([[c, -s], [s, c]], dtype=float)


def state_transition_matrix(dt):
    return np.array(
        [
            [1.0, 0.0, dt, 0.0],
            [0.0, 1.0, 0.0, dt],
            [0.0, 0.0, 1.0, 0.0],
            [0.0, 0.0, 0.0, 1.0],
        ],
        dtype=float,
    )


def control_matrix(dt):
    return np.array(
        [
            [0.5 * dt * dt, 0.0],
            [0.0, 0.5 * dt * dt],
            [dt, 0.0],
            [0.0, dt],
        ],
        dtype=float,
    )


def process_noise_matrix(dt, accel_std):
    """Q = B Qa B^T for a discrete per-step acceleration covariance."""
    b_mat = control_matrix(dt)
    q_accel = np.diag([accel_std**2, accel_std**2])
    return b_mat @ q_accel @ b_mat.T


def sym(P):
    return 0.5 * (P + P.T)


def ekf_propagate(x, P, u_world, dt, Q):
    """EKF prediction. No ground truth is accepted by this function."""
    F = state_transition_matrix(dt)
    B = control_matrix(dt)
    x_next = F @ x + B @ u_world
    P_next = F @ P @ F.T + Q
    return x_next, sym(P_next)


def range_prediction(x, anchor):
    delta = np.asarray(x[:2], dtype=float) - np.asarray(anchor, dtype=float)
    return float(np.linalg.norm(delta))


def range_jacobian(x, anchor):
    """Jacobian of scalar range; coincident target/anchor is rejected."""
    delta = np.asarray(x[:2], dtype=float) - np.asarray(anchor, dtype=float)
    r = float(np.linalg.norm(delta))
    if not np.isfinite(r) or r <= RANGE_SINGULAR_TOL:
        raise ValueError("range observation is singular at the anchor; update rejected")
    return np.array([[delta[0] / r, delta[1] / r, 0.0, 0.0]], dtype=float)


def range_ekf_update(x, P, z, anchor, R):
    """Scalar Gaussian range update with Joseph covariance."""
    if not np.isfinite(z) or not np.isfinite(R) or R <= 0.0:
        raise ValueError("range measurement and variance must be finite; R must be positive")
    H = range_jacobian(x, anchor)
    innovation = float(z - range_prediction(x, anchor))
    S = float((H @ P @ H.T + R).item())
    if not np.isfinite(S) or S <= 0.0:
        raise ValueError("invalid innovation covariance")
    K = (P @ H.T) / S
    x_next = x + (K[:, 0] * innovation)
    A = np.eye(4) - K @ H
    P_next = A @ P @ A.T + K * R @ K.T
    return x_next, sym(P_next)


def true_kinematics(t):
    """Analytic smooth circular motion used only by the synthetic simulator."""
    theta = OMEGA * t
    c = math.cos(theta)
    s = math.sin(theta)
    pos = CENTER + RADIUS * np.array([c, s], dtype=float)
    vel = RADIUS * OMEGA * np.array([-s, c], dtype=float)
    acc_world = -RADIUS * OMEGA**2 * np.array([c, s], dtype=float)
    yaw = math.atan2(vel[1], vel[0])
    return pos, vel, acc_world, yaw


def run_self_check():
    started = time.perf_counter()

    # 1) Analytic range Jacobian against centered finite differences.
    x_check = np.array([1.2, -0.7, 0.4, -0.2], dtype=float)
    anchor = np.array([3.0, 1.5], dtype=float)
    H = range_jacobian(x_check, anchor)
    eps = 1e-6
    H_num = np.zeros_like(H)
    for i in range(4):
        step = np.zeros(4)
        step[i] = eps
        h_plus = range_prediction(x_check + step, anchor)
        h_minus = range_prediction(x_check - step, anchor)
        H_num[0, i] = (h_plus - h_minus) / (2.0 * eps)
    jac_err = float(np.max(np.abs(H - H_num)))
    if jac_err > 5e-7:
        raise RuntimeError("range Jacobian finite-difference check failed")

    # 2) Exact constant-acceleration propagation.
    x0 = np.array([0.2, -0.1, 0.7, 0.4], dtype=float)
    u = np.array([0.8, -0.5], dtype=float)
    x_pred, _ = ekf_propagate(x0, np.eye(4), u, DT, np.zeros((4, 4)))
    expected = x0 + np.array(
        [
            x0[2] * DT + 0.5 * u[0] * DT**2,
            x0[3] * DT + 0.5 * u[1] * DT**2,
            u[0] * DT,
            u[1] * DT,
        ]
    )
    propagation_err = float(np.max(np.abs(x_pred - expected)))
    if propagation_err > 1e-12:
        raise RuntimeError("constant-acceleration propagation check failed")

    # 3) Joseph covariance remains finite, symmetric, and PSD after a sequence.
    x_cov = np.array([2.0, -1.0, 0.4, 0.2], dtype=float)
    P_cov = np.diag([0.5**2, 0.5**2, 0.2**2, 0.2**2])
    Q = process_noise_matrix(DT, PROCESS_ACCEL_SIGMA)
    for i in range(30):
        u_i = np.array([0.08 * math.sin(0.2 * i), 0.06 * math.cos(0.17 * i)])
        x_cov, P_cov = ekf_propagate(x_cov, P_cov, u_i, DT, Q)
        anchor_i = ANCHORS[i % len(ANCHORS)]
        z_i = range_prediction(x_cov, anchor_i) + 0.03 * math.sin(i)
        x_cov, P_cov = range_ekf_update(x_cov, P_cov, z_i, anchor_i, RANGE_SIGMA**2)
    finite_ok = bool(np.all(np.isfinite(x_cov)) and np.all(np.isfinite(P_cov)))
    symmetry_err = float(np.max(np.abs(P_cov - P_cov.T)))
    eigenvalues = np.linalg.eigvalsh(P_cov)
    min_eig = float(np.min(eigenvalues))
    if not finite_ok or symmetry_err > 1e-9 or min_eig < -1e-9:
        raise RuntimeError("Joseph covariance check failed")

    # 4) A coincident target/anchor must be rejected, not silently linearized.
    singular_rejected = False
    try:
        range_ekf_update(
            np.array([1.0, 1.0, 0.0, 0.0]),
            np.eye(4),
            0.0,
            np.array([1.0, 1.0]),
            RANGE_SIGMA**2,
        )
    except ValueError:
        singular_rejected = True
    if not singular_rejected:
        raise RuntimeError("singular range update was not rejected")

    elapsed = time.perf_counter() - started
    print(
        f"{LABEL} self-check: PASS | runtime={elapsed:.3f}s | "
        f"jac_err={jac_err:.2e} | Joseph_min_eig={min_eig:.2e}"
    )


def simulate_and_filter(seed):
    rng = np.random.default_rng(seed)
    n_steps = int(round(DURATION / DT))
    times = np.arange(n_steps + 1, dtype=float) * DT

    gt = np.zeros((n_steps + 1, 4), dtype=float)
    for k, t in enumerate(times):
        pos, vel, _, _ = true_kinematics(t)
        gt[k, :2] = pos
        gt[k, 2:] = vel

    x_init = NOMINAL_STATE + INITIAL_PERTURBATION
    x_est = x_init.copy()
    x_dead = x_init.copy()
    P_est = INITIAL_COV.copy()
    P_dead = INITIAL_COV.copy()
    Q = process_noise_matrix(DT, PROCESS_ACCEL_SIGMA)

    estimates = np.zeros((n_steps + 1, 4), dtype=float)
    dead_reckoning = np.zeros((n_steps + 1, 4), dtype=float)
    estimates[0] = x_est
    dead_reckoning[0] = x_dead
    u_history = np.zeros((n_steps, 2), dtype=float)
    range_update_flags = np.zeros(n_steps + 1, dtype=np.int64)

    next_range_time = RANGE_PERIOD
    range_epochs = 0
    scalar_ranges = 0

    for k in range(n_steps):
        _, _, acc_world_true, yaw_true = true_kinematics(times[k])
        acc_body_true = rotation_matrix(-yaw_true) @ acc_world_true
        acc_body_meas = acc_body_true + rng.normal(0.0, ACCEL_SIGMA, size=2)
        yaw_meas = wrap_angle(yaw_true + rng.normal(0.0, YAW_SIGMA))
        u_world_meas = rotation_matrix(yaw_meas) @ acc_body_meas
        u_history[k] = u_world_meas

        x_est, P_est = ekf_propagate(x_est, P_est, u_world_meas, DT, Q)
        x_dead, P_dead = ekf_propagate(x_dead, P_dead, u_world_meas, DT, Q)

        if times[k + 1] + 1e-12 >= next_range_time:
            for anchor in ANCHORS:
                true_range = float(np.linalg.norm(gt[k + 1, :2] - anchor))
                z_range = true_range + rng.normal(0.0, RANGE_SIGMA)
                x_est, P_est = range_ekf_update(
                    x_est, P_est, z_range, anchor, RANGE_SIGMA**2
                )
                scalar_ranges += 1
            range_update_flags[k + 1] = 1
            range_epochs += 1
            next_range_time += RANGE_PERIOD

        estimates[k + 1] = x_est
        dead_reckoning[k + 1] = x_dead

    ekf_error = np.linalg.norm(estimates[:, :2] - gt[:, :2], axis=1)
    dead_error = np.linalg.norm(dead_reckoning[:, :2] - gt[:, :2], axis=1)
    metrics = {
        "ekf_rmse_m": float(np.sqrt(np.mean(ekf_error**2))),
        "ekf_final_error_m": float(ekf_error[-1]),
        "ekf_max_error_m": float(np.max(ekf_error)),
        "dead_reckoning_rmse_m": float(np.sqrt(np.mean(dead_error**2))),
        "dead_reckoning_final_error_m": float(dead_error[-1]),
    }
    return {
        "times": times,
        "gt": gt,
        "estimates": estimates,
        "dead_reckoning": dead_reckoning,
        "u_history": u_history,
        "range_update_flags": range_update_flags,
        "ekf_error": ekf_error,
        "dead_error": dead_error,
        "metrics": metrics,
        "range_epochs": range_epochs,
        "scalar_ranges": scalar_ranges,
        "x_init": x_init,
    }


def write_csv(path, result):
    times = result["times"]
    gt = result["gt"]
    est = result["estimates"]
    dead = result["dead_reckoning"]
    ekf_error = result["ekf_error"]
    dead_error = result["dead_error"]
    flags = result["range_update_flags"]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "dataset",
                "time_s",
                "gt_px_m",
                "gt_py_m",
                "ekf_px_m",
                "ekf_py_m",
                "ekf_vx_mps",
                "ekf_vy_mps",
                "dead_px_m",
                "dead_py_m",
                "ekf_error_m",
                "dead_error_m",
                "range_update_epoch",
            ]
        )
        for k, t in enumerate(times):
            writer.writerow(
                [
                    LABEL,
                    f"{t:.6f}",
                    f"{gt[k, 0]:.6f}",
                    f"{gt[k, 1]:.6f}",
                    f"{est[k, 0]:.6f}",
                    f"{est[k, 1]:.6f}",
                    f"{est[k, 2]:.6f}",
                    f"{est[k, 3]:.6f}",
                    f"{dead[k, 0]:.6f}",
                    f"{dead[k, 1]:.6f}",
                    f"{ekf_error[k]:.6f}",
                    f"{dead_error[k]:.6f}",
                    int(flags[k]),
                ]
            )


def write_plot(path, result):
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    times = result["times"]
    gt = result["gt"]
    est = result["estimates"]
    dead = result["dead_reckoning"]
    fig, (ax_traj, ax_err) = plt.subplots(
        2, 1, figsize=(9.0, 8.2), constrained_layout=True
    )
    ax_traj.plot(gt[:, 0], gt[:, 1], "k-", linewidth=2.0, label="synthetic truth")
    ax_traj.plot(est[:, 0], est[:, 1], "C0-", linewidth=1.6, label="EKF")
    ax_traj.plot(
        dead[:, 0], dead[:, 1], "C1--", linewidth=1.2, label="IMU dead reckoning"
    )
    ax_traj.scatter(
        ANCHORS[:, 0],
        ANCHORS[:, 1],
        marker="^",
        s=70,
        c="C3",
        edgecolors="black",
        zorder=5,
        label="UWB anchors",
    )
    for i, anchor in enumerate(ANCHORS):
        ax_traj.annotate(
            f"A{i + 1}",
            (anchor[0], anchor[1]),
            xytext=(4, 4),
            textcoords="offset points",
            fontsize=8,
        )
    ax_traj.set_xlabel("world x (m)")
    ax_traj.set_ylabel("world y (m)")
    ax_traj.set_title("Synthetic trajectory and anchors")
    ax_traj.set_aspect("equal", adjustable="box")
    ax_traj.grid(True, alpha=0.3)
    ax_traj.legend(loc="best", fontsize=8)

    ax_err.plot(times, result["ekf_error"], "C0-", label="EKF position error")
    ax_err.plot(
        times, result["dead_error"], "C1--", label="dead-reckoning position error"
    )
    ax_err.set_xlabel("time (s)")
    ax_err.set_ylabel("position error (m)")
    ax_err.set_title("Offline error against synthetic truth")
    ax_err.grid(True, alpha=0.3)
    ax_err.legend(loc="best", fontsize=8)

    fig.suptitle(f"{LABEL}: planar UWB range + measured-IMU EKF", fontsize=12)
    fig.savefig(path, dpi=160)
    plt.close(fig)


def write_summary(path, result):
    summary = {
        "label": LABEL,
        "synthetic": True,
        "purpose": "Educational planar EKF example; not a production or research implementation.",
        "seed": SEED,
        "duration_s": DURATION,
        "dt_s": DT,
        "range_period_s": RANGE_PERIOD,
        "motion": "smooth synthetic circular path",
        "state": ["px_m", "py_m", "vx_mps", "vy_mps"],
        "anchors_m": ANCHORS.tolist(),
        "sensor_noise_std": {
            "body_acceleration_mps2": ACCEL_SIGMA,
            "yaw_rad": YAW_SIGMA,
            "uwb_range_m": RANGE_SIGMA,
            "discrete_process_acceleration_mps2": PROCESS_ACCEL_SIGMA,
        },
        "range_update_epochs": int(result["range_epochs"]),
        "scalar_range_measurements": int(result["scalar_ranges"]),
        "initial_state": {
            "value": result["x_init"].tolist(),
            "assumption": "fixed nominal pose plus small perturbation, independent of noisy ranges; educational known-start only",
        },
        "assumptions": [
            "externally supplied yaw measurement",
            "2D gravity already removed",
            "UWB and IMU clocks are aligned",
            "zero-mean Gaussian noise only",
            "not a full INS or attitude estimator",
        ],
        "metrics": result["metrics"],
        "outputs": {
            "plot": "synthetic_demo.png",
            "states_csv": "synthetic_states.csv",
            "summary_json": "summary.json",
        },
        "not_for": [
            "real data or CIR processing",
            "NLOS or multipath robustness claims",
            "learned or heavy-tailed measurement models",
            "adaptive risk, IMM, or production calibration",
            "safety-critical navigation",
            "comparison with any external research system",
        ],
    }
    path.write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def run_demo(out_dir):
    out_path = Path(out_dir)
    if out_path.exists():
        raise SystemExit(f"Refusing to write: output path already exists: {out_path}")
    out_path.mkdir(parents=True, exist_ok=False)

    started = time.perf_counter()
    result = simulate_and_filter(SEED)
    write_csv(out_path / "synthetic_states.csv", result)
    write_summary(out_path / "summary.json", result)
    write_plot(out_path / "synthetic_demo.png", result)
    elapsed = time.perf_counter() - started
    metrics = result["metrics"]
    print(
        f"{LABEL} demo: PASS | runtime={elapsed:.2f}s | "
        f"EKF RMSE={metrics['ekf_rmse_m']:.3f} m | "
        f"dead-reckoning RMSE={metrics['dead_reckoning_rmse_m']:.3f} m | "
        f"final EKF={metrics['ekf_final_error_m']:.3f} m | "
        f"{result['range_epochs']} range epochs/{result['scalar_ranges']} scalar ranges | "
        f"out={out_path}"
    )


def main():
    parser = argparse.ArgumentParser(
        description="Synthetic-only planar UWB range + measured-IMU EKF teaching demo."
    )
    parser.add_argument(
        "--self-check",
        action="store_true",
        help="run analytic/check numerical self-tests without writing output",
    )
    parser.add_argument(
        "--out",
        help="fresh output directory; refused if it already exists",
    )
    args = parser.parse_args()

    if args.self_check:
        run_self_check()
        return
    if not args.out:
        parser.error("--out is required for the demo; use --self-check for checks only")
    run_demo(args.out)


if __name__ == "__main__":
    main()