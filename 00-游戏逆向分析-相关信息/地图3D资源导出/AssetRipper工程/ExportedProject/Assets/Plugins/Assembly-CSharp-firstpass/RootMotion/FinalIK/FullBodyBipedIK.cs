using UnityEngine;

namespace RootMotion.FinalIK
{
	public class FullBodyBipedIK : IK
	{
		public BipedReferences references;

		public IKSolverFullBodyBiped solver;

		protected override void OpenUserManual()
		{
		}

		protected override void OpenScriptReference()
		{
		}

		private void OpenSetupTutorial()
		{
		}

		private void OpenInspectorTutorial()
		{
		}

		private void SupportGroup()
		{
		}

		private void ASThread()
		{
		}

		public void SetReferences(BipedReferences references, Transform rootNode)
		{
		}

		public override IKSolver GetIKSolver()
		{
			return null;
		}

		public bool ReferencesError(ref string errorMessage)
		{
			return false;
		}

		public bool ReferencesWarning(ref string warningMessage)
		{
			return false;
		}

		private void Reinitiate()
		{
		}

		private void AutoDetectReferences()
		{
		}
	}
}
