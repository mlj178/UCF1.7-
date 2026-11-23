using UnityEngine;

namespace RootMotion.FinalIK
{
	public class RotationLimitHinge : RotationLimit
	{
		public bool useLimits;

		public float min;

		public float max;

		[HideInInspector]
		public float zeroAxisDisplayOffset;

		private Quaternion lastRotation;

		private float lastAngle;

		private void OpenUserManual()
		{
		}

		private void OpenScriptReference()
		{
		}

		private void SupportGroup()
		{
		}

		private void ASThread()
		{
		}

		protected override Quaternion LimitRotation(Quaternion rotation)
		{
			return default;
		}

		private Quaternion LimitHinge(Quaternion rotation)
		{
			return default;
		}
	}
}
