using UnityEngine;

namespace RootMotion
{
	public class AxisTools
	{
		public static Vector3 ToVector3(Axis axis)
		{
			return default;
		}

		public static Axis ToAxis(Vector3 v)
		{
			return Axis.X;
		}

		public static Axis GetAxisToPoint(Transform t, Vector3 worldPosition)
		{
			return Axis.X;
		}

		public static Axis GetAxisToDirection(Transform t, Vector3 direction)
		{
			return Axis.X;
		}

		public static Vector3 GetAxisVectorToPoint(Transform t, Vector3 worldPosition)
		{
			return default;
		}

		public static Vector3 GetAxisVectorToDirection(Transform t, Vector3 direction)
		{
			return default;
		}

		public static Vector3 GetAxisVectorToDirection(Quaternion r, Vector3 direction)
		{
			return default;
		}
	}
}
