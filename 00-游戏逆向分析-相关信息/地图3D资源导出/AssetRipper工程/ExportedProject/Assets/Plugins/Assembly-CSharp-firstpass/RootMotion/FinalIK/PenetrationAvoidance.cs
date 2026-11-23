using System;
using UnityEngine;

namespace RootMotion.FinalIK
{
	public class PenetrationAvoidance : OffsetModifier
	{
		[Serializable]
		public class Avoider
		{
			[Serializable]
			public class EffectorLink
			{
				public FullBodyBipedEffector effector;

				public float weight;
			}

			public Transform[] raycastFrom;

			public Transform raycastTo;

			public float raycastRadius;

			public EffectorLink[] effectors;

			public float smoothTimeIn;

			public float smoothTimeOut;

			public LayerMask layers;

			private Vector3 offset;

			private Vector3 offsetTarget;

			private Vector3 offsetV;

			public void Solve(IKSolverFullBodyBiped solver, float weight)
			{
			}

			private Vector3 GetOffsetTarget(IKSolverFullBodyBiped solver)
			{
				return default;
			}

			private Vector3 Raycast(Vector3 from, Vector3 to)
			{
				return default;
			}
		}

		public Avoider[] avoiders;

		protected override void OnModifyOffset()
		{
		}
	}
}
