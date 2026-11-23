using UnityEngine;

namespace RootMotion.FinalIK
{
	public class RotationLimitSpline : RotationLimit
	{
		public float twistLimit;

		[SerializeField]
		[HideInInspector]
		public AnimationCurve spline;

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

		public void SetSpline(Keyframe[] keyframes)
		{
		}

		protected override Quaternion LimitRotation(Quaternion rotation)
		{
			return default;
		}

		public Quaternion LimitSwing(Quaternion rotation)
		{
			return default;
		}
	}
}
