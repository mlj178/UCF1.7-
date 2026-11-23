using UnityEngine;

namespace RootMotion.FinalIK
{
	public abstract class Grounder : MonoBehaviour
	{
		public delegate void GrounderDelegate();

		public float weight;

		public Grounding solver;

		public GrounderDelegate OnPreGrounder;

		public GrounderDelegate OnPostGrounder;

		public bool initiated { get; protected set; }

		public abstract void ResetPosition();

		protected Vector3 GetSpineOffsetTarget()
		{
			return default;
		}

		protected void LogWarning(string message)
		{
		}

		private Vector3 GetLegSpineBendVector(Grounding.Leg leg)
		{
			return default;
		}

		private Vector3 GetLegSpineTangent(Grounding.Leg leg)
		{
			return default;
		}

		protected abstract void OpenUserManual();

		protected abstract void OpenScriptReference();
	}
}
