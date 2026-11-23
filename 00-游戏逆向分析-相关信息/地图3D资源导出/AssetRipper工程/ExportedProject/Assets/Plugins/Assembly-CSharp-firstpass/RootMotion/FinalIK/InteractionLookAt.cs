using System;
using UnityEngine;

namespace RootMotion.FinalIK
{
	[Serializable]
	public class InteractionLookAt
	{
		public LookAtIK ik;

		public float lerpSpeed;

		public float weightSpeed;

		[HideInInspector]
		public bool isPaused;

		private Transform lookAtTarget;

		private float stopLookTime;

		private float weight;

		private bool firstFBBIKSolve;

		public void Look(Transform target, float time)
		{
		}

		public void OnFixTransforms()
		{
		}

		public void Update()
		{
		}

		public void SolveSpine()
		{
		}

		public void SolveHead()
		{
		}
	}
}
