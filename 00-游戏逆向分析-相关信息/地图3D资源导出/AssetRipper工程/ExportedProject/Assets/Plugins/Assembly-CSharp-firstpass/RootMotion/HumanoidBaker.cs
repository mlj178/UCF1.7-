using UnityEngine;

namespace RootMotion
{
	public class HumanoidBaker : Baker
	{
		public bool bakeHandIK;

		public float IKKeyReductionError;

		public int muscleFrameRateDiv;

		private BakerMuscle[] bakerMuscles;

		private BakerHumanoidQT rootQT;

		private BakerHumanoidQT leftFootQT;

		private BakerHumanoidQT rightFootQT;

		private BakerHumanoidQT leftHandQT;

		private BakerHumanoidQT rightHandQT;

		private float[] muscles;

		private HumanPose pose;

		private HumanPoseHandler handler;

		private Vector3 bodyPosition;

		private Quaternion bodyRotation;

		private int mN;

		private Quaternion lastBodyRotation;

		private void Awake()
		{
		}

		protected override Transform GetCharacterRoot()
		{
			return null;
		}

		protected override void OnStartBaking()
		{
		}

		protected override void OnSetLoopFrame(float time)
		{
		}

		protected override void OnSetCurves(ref AnimationClip clip)
		{
		}

		protected override void OnSetKeyframes(float time, bool lastFrame)
		{
		}

		private void UpdateHumanPose()
		{
		}
	}
}
