using System.Collections;
using UnityEngine;

namespace RootMotion.FinalIK
{
	public class AimController : MonoBehaviour
	{
		public AimIK ik;

		public float weight;

		public Transform target;

		public float targetSwitchSmoothTime;

		public float weightSmoothTime;

		public bool smoothTurnTowardsTarget;

		public float maxRadiansDelta;

		public float maxMagnitudeDelta;

		public float slerpSpeed;

		public Vector3 pivotOffsetFromRoot;

		public float minDistance;

		public Vector3 offset;

		public float maxRootAngle;

		public bool turnToTarget;

		public float turnToTargetTime;

		public bool useAnimatedAimDirection;

		public Vector3 animatedAimDirection;

		private Transform lastTarget;

		private float switchWeight;

		private float switchWeightV;

		private float weightV;

		private Vector3 lastPosition;

		private Vector3 dir;

		private bool lastSmoothTowardsTarget;

		private bool turningToTarget;

		private float turnToTargetMlp;

		private float turnToTargetMlpV;

		private Vector3 pivot => default;

		private void Start()
		{
		}

		private void LateUpdate()
		{
		}

		private void ApplyMinDistance()
		{
		}

		private void RootRotation()
		{
		}

		private IEnumerator TurnToTarget()
		{
			return null;
		}
	}
}
