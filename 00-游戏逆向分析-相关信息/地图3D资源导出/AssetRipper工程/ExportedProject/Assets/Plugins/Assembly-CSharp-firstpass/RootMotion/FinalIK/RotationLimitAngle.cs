using UnityEngine;

namespace RootMotion.FinalIK
{
	public class RotationLimitAngle : RotationLimit
	{
		public float limit;

		public float twistLimit;

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

		private Quaternion LimitSwing(Quaternion rotation)
		{
			return default;
		}
	}
}
