using UnityEngine;

namespace RootMotion.FinalIK
{
	public class BipedIK : SolverManager
	{
		public BipedReferences references;

		public BipedIKSolvers solvers;

		private void OpenUserManual()
		{
		}

		private void OpenScriptReference()
		{
		}

		private void SupportGroup()
		{
		}

		private void ASThread()
		{
		}

		public float GetIKPositionWeight(AvatarIKGoal goal)
		{
			return 0f;
		}

		public float GetIKRotationWeight(AvatarIKGoal goal)
		{
			return 0f;
		}

		public void SetIKPositionWeight(AvatarIKGoal goal, float weight)
		{
		}

		public void SetIKRotationWeight(AvatarIKGoal goal, float weight)
		{
		}

		public void SetIKPosition(AvatarIKGoal goal, Vector3 IKPosition)
		{
		}

		public void SetIKRotation(AvatarIKGoal goal, Quaternion IKRotation)
		{
		}

		public Vector3 GetIKPosition(AvatarIKGoal goal)
		{
			return default;
		}

		public Quaternion GetIKRotation(AvatarIKGoal goal)
		{
			return default;
		}

		public void SetLookAtWeight(float weight, float bodyWeight, float headWeight, float eyesWeight, float clampWeight, float clampWeightHead, float clampWeightEyes)
		{
		}

		public void SetLookAtPosition(Vector3 lookAtPosition)
		{
		}

		public void SetSpinePosition(Vector3 spinePosition)
		{
		}

		public void SetSpineWeight(float weight)
		{
		}

		public IKSolverLimb GetGoalIK(AvatarIKGoal goal)
		{
			return null;
		}

		public void InitiateBipedIK()
		{
		}

		public void UpdateBipedIK()
		{
		}

		public void SetToDefaults()
		{
		}

		protected override void FixTransforms()
		{
		}

		protected override void InitiateSolver()
		{
		}

		protected override void UpdateSolver()
		{
		}

		public void LogWarning(string message)
		{
		}
	}
}
