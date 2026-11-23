using UnityEngine;

namespace RootMotion.FinalIK
{
	public class GrounderIK : Grounder
	{
		public IK[] legs;

		public Transform pelvis;

		public Transform characterRoot;

		public float rootRotationWeight;

		public float rootRotationSpeed;

		public float maxRootRotationAngle;

		private Transform[] feet;

		private Quaternion[] footRotations;

		private Vector3 animatedPelvisLocalPosition;

		private Vector3 solvedPelvisLocalPosition;

		private int solvedFeet;

		private bool solved;

		private float lastWeight;

		private Rigidbody characterRootRigidbody;

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

		private void OnDisable()
		{
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

		private void SetLegIK(int index)
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
