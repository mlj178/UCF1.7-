using UnityEngine;

namespace RootMotion.FinalIK
{
	public class GrounderQuadruped : Grounder
	{
		public struct Foot
		{
			public IKSolver solver;

			public Transform transform;

			public Quaternion rotation;

			public Grounding.Leg leg;

			public Foot(IKSolver solver, Transform transform)
			{
				this.solver = null;
				this.transform = null;
				rotation = default;
				leg = null;
			}
		}

		public Grounding forelegSolver;

		public float rootRotationWeight;

		public float minRootRotation;

		public float maxRootRotation;

		public float rootRotationSpeed;

		public float maxLegOffset;

		public float maxForeLegOffset;

		public float maintainHeadRotationWeight;

		public Transform characterRoot;

		public Transform pelvis;

		public Transform lastSpineBone;

		public Transform head;

		public IK[] legs;

		public IK[] forelegs;

		[HideInInspector]
		public Vector3 gravity;

		private Foot[] feet;

		private Vector3 animatedPelvisLocalPosition;

		private Quaternion animatedPelvisLocalRotation;

		private Quaternion animatedHeadLocalRotation;

		private Vector3 solvedPelvisLocalPosition;

		private Quaternion solvedPelvisLocalRotation;

		private Quaternion solvedHeadLocalRotation;

		private int solvedFeet;

		private bool solved;

		private float angle;

		private Transform forefeetRoot;

		private Quaternion headRotation;

		private float lastWeight;

		private Rigidbody characterRootRigidbody;

		protected override void OpenUserManual()
		{
		}

		protected override void OpenScriptReference()
		{
		}

		public override void ResetPosition()
		{
		}

		private bool IsReadyToInitiate()
		{
			return false;
		}

		private bool IsReadyToInitiateLegs(IK[] ikComponents)
		{
			return false;
		}

		private void OnDisable()
		{
		}

		private void Update()
		{
		}

		private void Initiate()
		{
		}

		private Transform[] InitiateFeet(IK[] ikComponents, ref Foot[] f, int indexOffset)
		{
			return null;
		}

		private void LateUpdate()
		{
		}

		private void RootRotation()
		{
		}

		private void OnSolverUpdate()
		{
		}

		private void UpdateForefeetRoot()
		{
		}

		private void SetFootIK(Foot foot, float maxOffset)
		{
		}

		private void OnPostSolverUpdate()
		{
		}

		private void OnDestroy()
		{
		}

		private void DestroyLegs(IK[] ikComponents)
		{
		}
	}
}
