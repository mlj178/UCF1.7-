using System;
using UnityEngine;

namespace RootMotion.FinalIK
{
	[Serializable]
	public class IKSolverAim : IKSolverHeuristic
	{
		public Transform transform;

		public Vector3 axis;

		public Vector3 poleAxis;

		public Vector3 polePosition;

		public float poleWeight;

		public Transform poleTarget;

		public float clampWeight;

		public int clampSmoothing;

		public IterationDelegate OnPreIteration;

		private float step;

		private Vector3 clampedIKPosition;

		private RotationLimit transformLimit;

		private Transform lastTransform;

		public Vector3 transformAxis => default;

		public Vector3 transformPoleAxis => default;

		protected override int minBones => 0;

		protected override Vector3 localDirection => default;

		public float GetAngle()
		{
			return 0f;
		}

		protected override void OnInitiate()
		{
		}

		protected override void OnUpdate()
		{
		}

		private void Solve()
		{
		}

		private Vector3 GetClampedIKPosition()
		{
			return default;
		}

		private void RotateToTarget(Vector3 targetPosition, Bone bone, float weight)
		{
		}
	}
}
