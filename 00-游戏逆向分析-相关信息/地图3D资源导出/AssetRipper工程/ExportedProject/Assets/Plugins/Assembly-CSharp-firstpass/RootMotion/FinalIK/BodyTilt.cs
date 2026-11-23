using UnityEngine;

namespace RootMotion.FinalIK
{
	public class BodyTilt : OffsetModifier
	{
		public float tiltSpeed;

		public float tiltSensitivity;

		public OffsetPose poseLeft;

		public OffsetPose poseRight;

		private float tiltAngle;

		private Vector3 lastForward;

		protected override void Start()
		{
		}

		protected override void OnModifyOffset()
		{
		}
	}
}
