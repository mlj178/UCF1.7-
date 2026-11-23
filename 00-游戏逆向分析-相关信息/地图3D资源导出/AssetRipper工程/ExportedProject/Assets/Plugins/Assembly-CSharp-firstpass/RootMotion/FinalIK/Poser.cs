using UnityEngine;

namespace RootMotion.FinalIK
{
	public abstract class Poser : SolverManager
	{
		public Transform poseRoot;

		public float weight;

		public float localRotationWeight;

		public float localPositionWeight;

		private bool initiated;

		public abstract void AutoMapping();

		public void UpdateManual()
		{
		}

		protected abstract void InitiatePoser();

		protected abstract void UpdatePoser();

		protected abstract void FixPoserTransforms();

		protected override void UpdateSolver()
		{
		}

		protected override void InitiateSolver()
		{
		}

		protected override void FixTransforms()
		{
		}
	}
}
