using System;
using UnityEngine;

namespace RootMotion.FinalIK
{
	public class Inertia : OffsetModifier
	{
		[Serializable]
		public class Body
		{
			[Serializable]
			public class EffectorLink
			{
				public FullBodyBipedEffector effector;

				public float weight;
			}

			public Transform transform;

			public EffectorLink[] effectorLinks;

			public float speed;

			public float acceleration;

			public float matchVelocity;

			public float gravity;

			private Vector3 delta;

			private Vector3 lazyPoint;

			private Vector3 direction;

			private Vector3 lastPosition;

			private bool firstUpdate;

			public void Reset()
			{
			}

			public void Update(IKSolverFullBodyBiped solver, float weight, float deltaTime)
			{
			}
		}

		public Body[] bodies;

		public OffsetLimits[] limits;

		public void ResetBodies()
		{
		}

		protected override void OnModifyOffset()
		{
		}
	}
}
