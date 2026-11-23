using System;
using UnityEngine;

namespace RootMotion.FinalIK
{
	public class GrounderFBBIK : Grounder
	{
		[Serializable]
		public class SpineEffector
		{
			public FullBodyBipedEffector effectorType;

			public float horizontalWeight;

			public float verticalWeight;

			public SpineEffector()
			{
			}

			public SpineEffector(FullBodyBipedEffector effectorType, float horizontalWeight, float verticalWeight)
			{
			}
		}

		public FullBodyBipedIK ik;

		public float spineBend;

		public float spineSpeed;

		public SpineEffector[] spine;

		private Transform[] feet;

		private Vector3 spineOffset;

		private bool firstSolve;

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

		private void FixedUpdate()
		{
		}

		private void LateUpdate()
		{
		}

		private void Initiate()
		{
		}

		private void OnSolverUpdate()
		{
		}

		private void SetLegIK(IKEffector effector, Grounding.Leg leg)
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
