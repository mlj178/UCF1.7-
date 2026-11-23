using System;
using UnityEngine;

namespace RootMotion.FinalIK
{
	public class InteractionTrigger : MonoBehaviour
	{
		[Serializable]
		public class CharacterPosition
		{
			public bool use;

			public Vector2 offset;

			public float angleOffset;

			public float maxAngle;

			public float radius;

			public bool orbit;

			public bool fixYAxis;

			public Vector3 offset3D => default;

			public Vector3 direction3D => default;

			public bool IsInRange(Transform character, Transform trigger, out float error)
			{
				error = default;
				return false;
			}
		}

		[Serializable]
		public class CameraPosition
		{
			public Collider lookAtTarget;

			public Vector3 direction;

			public float maxDistance;

			public float maxAngle;

			public bool fixYAxis;

			public Quaternion GetRotation()
			{
				return default;
			}

			public bool IsInRange(Transform raycastFrom, RaycastHit hit, Transform trigger, out float error)
			{
				error = default;
				return false;
			}
		}

		[Serializable]
		public class Range
		{
			[Serializable]
			public class Interaction
			{
				public InteractionObject interactionObject;

				public FullBodyBipedEffector[] effectors;
			}

			[HideInInspector]
			[SerializeField]
			public string name;

			[HideInInspector]
			[SerializeField]
			public bool show;

			public CharacterPosition characterPosition;

			public CameraPosition cameraPosition;

			public Interaction[] interactions;

			public bool IsInRange(Transform character, Transform raycastFrom, RaycastHit raycastHit, Transform trigger, out float maxError)
			{
				maxError = default;
				return false;
			}
		}

		public Range[] ranges;

		private void OpenUserManual()
		{
		}

		private void OpenScriptReference()
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

		private void Start()
		{
		}

		public int GetBestRangeIndex(Transform character, Transform raycastFrom, RaycastHit raycastHit)
		{
			return 0;
		}
	}
}
