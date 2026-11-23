using UnityEngine;

namespace RootMotion
{
	public static class QuaTools
	{
		public static Quaternion Lerp(Quaternion fromRotation, Quaternion toRotation, float weight)
		{
			return default;
		}

		public static Quaternion Slerp(Quaternion fromRotation, Quaternion toRotation, float weight)
		{
			return default;
		}

		public static Quaternion LinearBlend(Quaternion q, float weight)
		{
			return default;
		}

		public static Quaternion SphericalBlend(Quaternion q, float weight)
		{
			return default;
		}

		public static Quaternion FromToAroundAxis(Vector3 fromDirection, Vector3 toDirection, Vector3 axis)
		{
			return default;
		}

		public static Quaternion RotationToLocalSpace(Quaternion space, Quaternion rotation)
		{
			return default;
		}

		public static Quaternion FromToRotation(Quaternion from, Quaternion to)
		{
			return default;
		}

		public static Vector3 GetAxis(Vector3 v)
		{
			return default;
		}

		public static Quaternion ClampRotation(Quaternion rotation, float clampWeight, int clampSmoothing)
		{
			return default;
		}

		public static float ClampAngle(float angle, float clampWeight, int clampSmoothing)
		{
			return 0f;
		}

		public static Quaternion MatchRotation(Quaternion targetRotation, Vector3 targetforwardAxis, Vector3 targetUpAxis, Vector3 forwardAxis, Vector3 upAxis)
		{
			return default;
		}

		public static Vector3 ToBiPolar(Vector3 euler)
		{
			return default;
		}

		public static float ToBiPolar(float angle)
		{
			return 0f;
		}
	}
}
