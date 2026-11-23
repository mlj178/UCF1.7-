using UnityEngine;

namespace RootMotion.FinalIK
{
	public class LookAtController : MonoBehaviour
	{
		public LookAtIK ik;

		public Transform target;

		public float weight;

		public Vector3 offset;

		public float targetSwitchSmoothTime;

		public float weightSmoothTime;

		public bool smoothTurnTowardsTarget;

		public float maxRadiansDelta;

		public float maxMagnitudeDelta;

		public float slerpSpeed;

		public Vector3 pivotOffsetFromRoot;

		public float minDistance;

		public float maxRootAngle;

		private Transform lastTarget;

		private float switchWeight;

		private float switchWeightV;

		private float weightV;

		private Vector3 lastPosition;

		private Vector3 dir;

		private bool lastSmoothTowardsTarget;

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
	}
}
