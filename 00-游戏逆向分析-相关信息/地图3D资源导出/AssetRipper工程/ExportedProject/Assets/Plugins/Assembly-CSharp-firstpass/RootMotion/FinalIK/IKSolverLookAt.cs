using System;
using UnityEngine;

namespace RootMotion.FinalIK
{
	[Serializable]
	public class IKSolverLookAt : IKSolver
	{
		[Serializable]
		public class LookAtBone : Bone
		{
			public Vector3 baseForwardOffsetEuler;

			public Vector3 forward => default;

			public LookAtBone()
			{
			}

			public LookAtBone(Transform transform)
			{
			}

			public void Initiate(Transform root)
			{
			}

			public void LookAt(Vector3 direction, float weight)
			{
			}
		}

		public Transform target;

		public LookAtBone[] spine;

		public LookAtBone head;

		public LookAtBone[] eyes;

		public float bodyWeight;

		public float headWeight;

		public float eyesWeight;

		public float clampWeight;

		public float clampWeightHead;

		public float clampWeightEyes;

		public int clampSmoothing;

		public AnimationCurve spineWeightCurve;

		public Vector3 spineTargetOffset;

		protected Vector3[] spineForwards;

		protected Vector3[] headForwards;

		protected Vector3[] eyeForward;

		protected bool spineIsValid => false;

		protected bool spineIsEmpty => false;

		protected bool headIsValid => false;

		protected bool headIsEmpty => false;

		protected bool eyesIsValid => false;

		protected bool eyesIsEmpty => false;

		public void SetLookAtWeight(float weight)
		{
		}

		public void SetLookAtWeight(float weight, float bodyWeight)
		{
		}

		public void SetLookAtWeight(float weight, float bodyWeight, float headWeight)
		{
		}

		public void SetLookAtWeight(float weight, float bodyWeight, float headWeight, float eyesWeight)
		{
		}

		public void SetLookAtWeight(float weight, float bodyWeight, float headWeight, float eyesWeight, float clampWeight)
		{
		}

		public void SetLookAtWeight(float weight, float bodyWeight = 0f, float headWeight = 1f, float eyesWeight = 0.5f, float clampWeight = 0.5f, float clampWeightHead = 0.5f, float clampWeightEyes = 0.3f)
		{
		}

		public override void StoreDefaultLocalState()
		{
		}

		public override void FixTransforms()
		{
		}

		public override bool IsValid(ref string message)
		{
			return false;
		}

		public override Point[] GetPoints()
		{
			return null;
		}

		public override Point GetPoint(Transform transform)
		{
			return null;
		}

		public bool SetChain(Transform[] spine, Transform head, Transform[] eyes, Transform root)
		{
			return false;
		}

		protected override void OnInitiate()
		{
		}

		protected override void OnUpdate()
		{
		}

		protected void SolveSpine()
		{
		}

		protected void SolveHead()
		{
		}

		protected void SolveEyes()
		{
		}

		protected Vector3[] GetForwards(ref Vector3[] forwards, Vector3 baseForward, Vector3 targetForward, int bones, float clamp)
		{
			return null;
		}

		protected void SetBones(Transform[] array, ref LookAtBone[] bones)
		{
		}
	}
}
