import numpy as np


def get_transformation_to_xz() -> np.ndarray:
    # Rotate +90 degrees around the Y-axis
    theta = np.pi / 2  # +90 degrees in radians
    rotation_matrix = (
        np.array(
            [
                [np.cos(theta), 0, -np.sin(theta), 0],
                [0, -1, 0, 0],
                [-np.sin(theta), 0, -np.cos(theta), 0],
            ]
        )
        * -1
    )
    return rotation_matrix


def get_transformation_to_zy() -> np.ndarray:
    # Rotate -90 degrees around the X-axis
    theta = -np.pi / 2  # -90 degrees in radians
    rotation_matrix = (
        np.array(
            [
                [-1, 0, 0, 0],
                [0, np.cos(theta), np.sin(theta), 0],
                [0, np.sin(theta), -np.cos(theta), 0],
            ]
        )
        * -1
    )
    return rotation_matrix
