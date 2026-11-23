using System;
using UnityEngine;

namespace RootMotion.FinalIK
{
	public class VRIK : IK
	{
		[Serializable]
		public class References
		{
			public Transform root;

			public Transform pelvis;

			public Transform spine;

			public Transform chest;

			public Transform neck;

			public Transform head;

			public Transform leftShoulder;

			public Transform leftUpperArm;

			public Transform leftForearm;

			public Transform leftHand;

			public Transform rightShoulder;

			public Transform rightUpperArm;

			public Transform rightForearm;

			public Transform rightHand;

			public Transform leftThigh;

			public Transform leftCalf;

			public Transform leftFoot;

			public Transform leftToes;

			public Transform rightThigh;

			public Transform rightCalf;

			public Transform rightFoot;

			public Transform rightToes;

			public bool isFilled => false;

			public bool isEmpty => false;

			public Transform[] GetTransforms()
			{
				return null;
			}

			public static bool AutoDetectReferences(Transform root, out References references)
			{
				references = null;
				return false;
			}
		}

		public References references;

		public IKSolverVR solver;

		protected override void OpenUserManual()
		{
		}

		protected override void OpenScriptReference()
		{
		}

		private void OpenSetupTutorial()
		{
		}

		public void AutoDetectReferences()
		{
		}

		public void GuessHandOrientations()
		{
		}

		public override IKSolver GetIKSolver()
		{
			return null;
		}

		protected override void InitiateSolver()
		{
		}

		protected override void UpdateSolver()
		{
		}
	}
}
