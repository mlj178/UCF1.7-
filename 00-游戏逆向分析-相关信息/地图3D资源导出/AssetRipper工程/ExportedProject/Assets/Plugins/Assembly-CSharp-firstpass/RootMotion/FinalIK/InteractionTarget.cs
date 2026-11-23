using System;
using UnityEngine;

namespace RootMotion.FinalIK
{
	public class InteractionTarget : MonoBehaviour
	{
		[Serializable]
		public class Multiplier
		{
			public InteractionObject.WeightCurve.Type curve;

			public float multiplier;
		}

		public FullBodyBipedEffector effectorType;

		public Multiplier[] multipliers;

		public float interactionSpeedMlp;

		public Transform pivot;

		public Vector3 twistAxis;

		public float twistWeight;

		public float swingWeight;

		public bool rotateOnce;

		private Quaternion defaultLocalRotation;

		private Transform lastPivot;

		private void OpenUserManual()
		{
		}

		private void OpenScriptReference()
		{
		}

		private void OpenTutorial1()
		{
		}

		private void OpenTutorial2()
		{
		}

		private void OpenTutorial3()
		{
		}

		private void OpenTutorial4()
		{
		}

		private void SupportGroup()
		{
		}

		private void ASThread()
		{
		}

		public float GetValue(InteractionObject.WeightCurve.Type curveType)
		{
			return 0f;
		}

		public void ResetRotation()
		{
		}

		public void RotateTo(Vector3 position)
		{
		}
	}
}
