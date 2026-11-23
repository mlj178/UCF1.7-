using System;
using UnityEngine;

namespace RootMotion.FinalIK
{
	public class RotationLimitPolygonal : RotationLimit
	{
		[Serializable]
		public class ReachCone
		{
			public Vector3[] tetrahedron;

			public float volume;

			public Vector3 S;

			public Vector3 B;

			public Vector3 o => default;

			public Vector3 a => default;

			public Vector3 b => default;

			public Vector3 c => default;

			public bool isValid => false;

			public ReachCone(Vector3 _o, Vector3 _a, Vector3 _b, Vector3 _c)
			{
			}

			public void Calculate()
			{
			}
		}

		[Serializable]
		public class LimitPoint
		{
			public Vector3 point;

			public float tangentWeight;
		}

		public float twistLimit;

		public int smoothIterations;

		[SerializeField]
		[HideInInspector]
		public LimitPoint[] points;

		[HideInInspector]
		[SerializeField]
		public Vector3[] P;

		[SerializeField]
		[HideInInspector]
		public ReachCone[] reachCones;

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

		public void SetLimitPoints(LimitPoint[] points)
		{
		}

		protected override Quaternion LimitRotation(Quaternion rotation)
		{
			return default;
		}

		private void Start()
		{
		}

		public void ResetToDefault()
		{
		}

		public void BuildReachCones()
		{
		}

		private Vector3[] SmoothPoints()
		{
			return null;
		}

		private float GetScalar(int k)
		{
			return 0f;
		}

		private Vector3 PointToTangentPlane(Vector3 p, float r)
		{
			return default;
		}

		private Vector3 TangentPointToSphere(Vector3 q, float r)
		{
			return default;
		}

		private Quaternion LimitSwing(Quaternion rotation)
		{
			return default;
		}

		private int GetReachCone(Vector3 L)
		{
			return 0;
		}
	}
}
