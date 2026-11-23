using System;
using UnityEngine;

namespace RootMotion.FinalIK
{
	public class FBBIKHeadEffector : MonoBehaviour
	{
		[Serializable]
		public class BendBone
		{
			public Transform transform;

			public float weight;

			private Quaternion defaultLocalRotation;

			public BendBone()
			{
			}

			public BendBone(Transform transform, float weight)
			{
			}

			public void StoreDefaultLocalState()
			{
			}

			public void FixTransforms()
			{
			}
		}

		public FullBodyBipedIK ik;

		public float positionWeight;

		public float bodyWeight;

		public float thighWeight;

		public bool handsPullBody;

		public float rotationWeight;

		public float bodyClampWeight;

		public float headClampWeight;

		public float bendWeight;

		public BendBone[] bendBones;

		public float CCDWeight;

		public float roll;

		public float damper;

		public Transform[] CCDBones;

		public float postStretchWeight;

		public float maxStretch;

		public float stretchDamper;

		public bool fixHead;

		public Transform[] stretchBones;

		public Vector3 chestDirection;

		public float chestDirectionWeight;

		public Transform[] chestBones;

		public IKSolver.UpdateDelegate OnPostHeadEffectorFK;

		private Vector3 offset;

		private Vector3 headToBody;

		private Vector3 shoulderCenterToHead;

		private Vector3 headToLeftThigh;

		private Vector3 headToRightThigh;

		private Vector3 leftShoulderPos;

		private Vector3 rightShoulderPos;

		private float shoulderDist;

		private float leftShoulderDist;

		private float rightShoulderDist;

		private Quaternion chestRotation;

		private Quaternion headRotationRelativeToRoot;

		private Quaternion[] ccdDefaultLocalRotations;

		private Vector3 headLocalPosition;

		private Quaternion headLocalRotation;

		private Vector3[] stretchLocalPositions;

		private Quaternion[] stretchLocalRotations;

		private Vector3[] chestLocalPositions;

		private Quaternion[] chestLocalRotations;

		private int bendBonesCount;

		private int ccdBonesCount;

		private int stretchBonesCount;

		private int chestBonesCount;

		private void Start()
		{
		}

		private void OnStoreDefaultLocalState()
		{
		}

		private void OnFixTransforms()
		{
		}

		private void OnPreRead()
		{
		}

		private void SpineBend()
		{
		}

		private void CCDPass()
		{
		}

		private void Iterate(int iteration)
		{
		}

		private void OnPostUpdate()
		{
		}

		private void ChestDirection()
		{
		}

		private void PostStretching()
		{
		}

		private void LerpSolverPosition(IKEffector effector, Vector3 position, float weight, Vector3 offset)
		{
		}

		private void Solve(ref Vector3 pos1, ref Vector3 pos2, float nominalDistance)
		{
		}

		private void OnDestroy()
		{
		}
	}
}
