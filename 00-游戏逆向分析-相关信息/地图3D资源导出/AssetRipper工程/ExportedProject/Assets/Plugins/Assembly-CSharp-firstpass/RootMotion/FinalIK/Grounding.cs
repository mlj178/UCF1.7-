using System;
using UnityEngine;

namespace RootMotion.FinalIK
{
	[Serializable]
	public class Grounding
	{
		[Serializable]
		public enum Quality
		{
			Fastest = 0,
			Simple = 1,
			Best = 2
		}

		public class Leg
		{
			public Quaternion rotationOffset;

			public bool invertFootCenter;

			private Grounding grounding;

			private float lastTime;

			private float deltaTime;

			private Vector3 lastPosition;

			private Quaternion toHitNormal;

			private Quaternion r;

			private Vector3 up;

			private bool doOverrideFootPosition;

			private Vector3 overrideFootPosition;

			private Vector3 transformPosition;

			public bool isGrounded { get; private set; }

			public Vector3 IKPosition { get; private set; }

			public bool initiated { get; private set; }

			public float heightFromGround { get; private set; }

			public Vector3 velocity { get; private set; }

			public Transform transform { get; private set; }

			public float IKOffset { get; private set; }

			public RaycastHit heelHit { get; private set; }

			public RaycastHit capsuleHit { get; private set; }

			public RaycastHit GetHitPoint => default;

			public float stepHeightFromGround => 0f;

			private float rootYOffset => 0f;

			public void SetFootPosition(Vector3 position)
			{
			}

			public void Initiate(Grounding grounding, Transform transform)
			{
			}

			public void OnEnable()
			{
			}

			public void Reset()
			{
			}

			public void Process()
			{
			}

			private RaycastHit GetCapsuleHit(Vector3 offsetFromHeel)
			{
				return default;
			}

			private RaycastHit GetRaycastHit(Vector3 offsetFromHeel)
			{
				return default;
			}

			private Vector3 RotateNormal(Vector3 normal)
			{
				return default;
			}

			private void SetFootToPoint(Vector3 normal, Vector3 point)
			{
			}

			private void SetFootToPlane(Vector3 planeNormal, Vector3 planePoint, Vector3 heelHitPoint)
			{
			}

			private float GetHeightFromGround(Vector3 hitPoint)
			{
				return 0f;
			}

			private void RotateFoot()
			{
			}

			private Quaternion GetRotationOffsetTarget()
			{
				return default;
			}
		}

		public class Pelvis
		{
			private Grounding grounding;

			private Vector3 lastRootPosition;

			private float damperF;

			private bool initiated;

			private float lastTime;

			public Vector3 IKOffset { get; private set; }

			public float heightOffset { get; private set; }

			public void Initiate(Grounding grounding)
			{
			}

			public void Reset()
			{
			}

			public void OnEnable()
			{
			}

			public void Process(float lowestOffset, float highestOffset, bool isGrounded)
			{
			}
		}

		public LayerMask layers;

		public float maxStep;

		public float heightOffset;

		public float footSpeed;

		public float footRadius;

		[HideInInspector]
		public float footCenterOffset;

		public float prediction;

		public float footRotationWeight;

		public float footRotationSpeed;

		public float maxFootRotationAngle;

		public bool rotateSolver;

		public float pelvisSpeed;

		public float pelvisDamper;

		public float lowerPelvisWeight;

		public float liftPelvisWeight;

		public float rootSphereCastRadius;

		public bool overstepFallsDown;

		public Quality quality;

		private bool initiated;

		public Leg[] legs { get; private set; }

		public Pelvis pelvis { get; private set; }

		public bool isGrounded { get; private set; }

		public Transform root { get; private set; }

		public RaycastHit rootHit { get; private set; }

		public bool rootGrounded => false;

		public Vector3 up => default;

		private bool useRootRotation => false;

		public RaycastHit GetRootHit(float maxDistanceMlp = 10f)
		{
			return default;
		}

		public bool IsValid(ref string errorMessage)
		{
			return false;
		}

		public void Initiate(Transform root, Transform[] feet)
		{
		}

		public void Update()
		{
		}

		public Vector3 GetLegsPlaneNormal()
		{
			return default;
		}

		public void Reset()
		{
		}

		public void LogWarning(string message)
		{
		}

		public float GetVerticalOffset(Vector3 p1, Vector3 p2)
		{
			return 0f;
		}

		public Vector3 Flatten(Vector3 v)
		{
			return default;
		}

		public Vector3 GetFootCenterOffset()
		{
			return default;
		}
	}
}
