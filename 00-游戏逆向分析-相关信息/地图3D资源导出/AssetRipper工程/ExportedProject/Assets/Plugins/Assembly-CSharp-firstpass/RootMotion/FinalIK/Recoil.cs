using System;
using UnityEngine;

namespace RootMotion.FinalIK
{
	public class Recoil : OffsetModifier
	{
		[Serializable]
		public class RecoilOffset
		{
			[Serializable]
			public class EffectorLink
			{
				public FullBodyBipedEffector effector;

				public float weight;
			}

			public Vector3 offset;

			public float additivity;

			public float maxAdditiveOffsetMag;

			public EffectorLink[] effectorLinks;

			private Vector3 additiveOffset;

			private Vector3 lastOffset;

			public void Start()
			{
			}

			public void Apply(IKSolverFullBodyBiped solver, Quaternion rotation, float masterWeight, float length, float timeLeft)
			{
			}
		}

		[Serializable]
		public enum Handedness
		{
			Right = 0,
			Left = 1
		}

		public AimIK aimIK;

		public bool aimIKSolvedLast;

		public Handedness handedness;

		public bool twoHanded;

		public AnimationCurve recoilWeight;

		public float magnitudeRandom;

		public Vector3 rotationRandom;

		public Vector3 handRotationOffset;

		public float blendTime;

		[Space]
		public RecoilOffset[] offsets;

		[HideInInspector]
		public Quaternion rotationOffset;

		private float magnitudeMlp;

		private float endTime;

		private Quaternion handRotation;

		private Quaternion secondaryHandRelativeRotation;

		private Quaternion randomRotation;

		private float length;

		private bool initiated;

		private float blendWeight;

		private float w;

		private Quaternion primaryHandRotation;

		private bool handRotationsSet;

		private Vector3 aimIKAxis;

		public bool isFinished => false;

		private IKEffector primaryHandEffector => null;

		private IKEffector secondaryHandEffector => null;

		private Transform primaryHand => null;

		private Transform secondaryHand => null;

		public void SetHandRotations(Quaternion leftHandRotation, Quaternion rightHandRotation)
		{
		}

		public void Fire(float magnitude)
		{
		}

		protected override void OnModifyOffset()
		{
		}

		private void AfterFBBIK()
		{
		}

		private void AfterAimIK()
		{
		}

		protected override void OnDestroy()
		{
		}
	}
}
