using System;
using UnityEngine;
using UnityEngine.AI;

namespace RootMotion.Demos
{
	[Serializable]
	public class Navigator
	{
		public enum State
		{
			Idle = 0,
			Seeking = 1,
			OnPath = 2
		}

		public bool activeTargetSeeking;

		public float cornerRadius;

		public float recalculateOnPathDistance;

		public float maxSampleDistance;

		public float nextPathInterval;

		private Transform transform;

		private int cornerIndex;

		private Vector3[] corners;

		private NavMeshPath path;

		private Vector3 lastTargetPosition;

		private bool initiated;

		private float nextPathTime;

		public Vector3 normalizedDeltaPosition { get; private set; }

		public State state { get; private set; }

		public void Initiate(Transform transform)
		{
		}

		public void Update(Vector3 targetPosition)
		{
		}

		private void CalculatePath(Vector3 targetPosition)
		{
		}

		private bool Find(Vector3 targetPosition)
		{
			return false;
		}

		private void Stop()
		{
		}

		private float HorDistance(Vector3 p1, Vector3 p2)
		{
			return 0f;
		}

		public void Visualize()
		{
		}
	}
}
