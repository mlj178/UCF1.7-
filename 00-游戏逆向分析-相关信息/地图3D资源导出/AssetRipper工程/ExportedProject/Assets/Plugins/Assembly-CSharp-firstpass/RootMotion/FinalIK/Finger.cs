using System;
using UnityEngine;

namespace RootMotion.FinalIK
{
	[Serializable]
	public class Finger
	{
		[Serializable]
		public enum DOF
		{
			One = 0,
			Three = 1
		}

		public float weight;

		public float rotationWeight;

		public DOF rotationDOF;

		public bool fixBone1Twist;

		public Transform bone1;

		public Transform bone2;

		public Transform bone3;

		public Transform tip;

		public Transform target;

		private IKSolverLimb solver;

		private Quaternion bone3RelativeToTarget;

		private Vector3 bone3DefaultLocalPosition;

		private Quaternion bone3DefaultLocalRotation;

		private Vector3 bone1Axis;

		private Vector3 tipAxis;

		private Vector3 bone1TwistAxis;

		public bool initiated { get; private set; }

		public Vector3 IKPosition
		{
			get
			{
				return default;
			}
			set
			{
			}
		}

		public Quaternion IKRotation
		{
			get
			{
				return default;
			}
			set
			{
			}
		}

		public bool IsValid(ref string errorMessage)
		{
			return false;
		}

		public void Initiate(Transform hand, int index)
		{
		}

		public void FixTransforms()
		{
		}

		public void StoreDefaultLocalState()
		{
		}

		public void Update(float masterWeight)
		{
		}
	}
}
