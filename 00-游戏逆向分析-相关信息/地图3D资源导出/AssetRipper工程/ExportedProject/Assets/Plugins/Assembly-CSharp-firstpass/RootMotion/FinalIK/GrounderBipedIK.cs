using UnityEngine;

namespace RootMotion.FinalIK
{
	public class GrounderBipedIK : Grounder
	{
		public BipedIK ik;

		public float spineBend;

		public float spineSpeed;

		private Transform[] feet;

		private Quaternion[] footRotations;

		private Vector3 animatedPelvisLocalPosition;

		private Vector3 solvedPelvisLocalPosition;

		private Vector3 spineOffset;

		private float lastWeight;

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

		private void OnDisable()
		{
		}

		private void OnSolverUpdate()
		{
		}

		private void SetLegIK(IKSolverLimb limb, int index)
		{
		}

		private void OnPostSolverUpdate()
		{
		}

		private void OnDestroy()
		{
		}
	}
}
