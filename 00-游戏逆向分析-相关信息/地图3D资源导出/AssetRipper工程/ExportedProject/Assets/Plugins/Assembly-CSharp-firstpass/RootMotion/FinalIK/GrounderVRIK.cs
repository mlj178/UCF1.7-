using UnityEngine;

namespace RootMotion.FinalIK
{
	public class GrounderVRIK : Grounder
	{
		public VRIK ik;

		private Transform[] feet;

		private void OpenTutorial()
		{
		}

		protected override void OpenUserManual()
		{
		}

		protected override void OpenScriptReference()
		{
		}

		public override void ResetPosition()
		{
		}

		private bool IsReadyToInitiate()
		{
			return false;
		}

		private void Update()
		{
		}

		private void Initiate()
		{
		}

		private void OnSolverUpdate()
		{
		}

		private void SetLegIK(IKSolverVR.PositionOffset positionOffset, Transform bone, Grounding.Leg leg)
		{
		}

		private void OnPostSolverUpdate()
		{
		}

		private void OnDrawGizmosSelected()
		{
		}

		private void OnDestroy()
		{
		}
	}
}
