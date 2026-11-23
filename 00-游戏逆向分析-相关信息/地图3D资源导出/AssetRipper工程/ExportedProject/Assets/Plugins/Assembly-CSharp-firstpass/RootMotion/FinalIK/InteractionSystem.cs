using System.Collections.Generic;
using UnityEngine;

namespace RootMotion.FinalIK
{
	public class InteractionSystem : MonoBehaviour
	{
		public delegate void InteractionDelegate(FullBodyBipedEffector effectorType, InteractionObject interactionObject);

		public delegate void InteractionEventDelegate(FullBodyBipedEffector effectorType, InteractionObject interactionObject, InteractionObject.InteractionEvent interactionEvent);

		public string targetTag;

		public float fadeInTime;

		public float speed;

		public float resetToDefaultsSpeed;

		public Collider characterCollider;

		public Transform FPSCamera;

		public LayerMask camRaycastLayers;

		public float camRaycastDistance;

		private List<InteractionTrigger> inContact;

		private List<int> bestRangeIndexes;

		public InteractionDelegate OnInteractionStart;

		public InteractionDelegate OnInteractionPause;

		public InteractionDelegate OnInteractionPickUp;

		public InteractionDelegate OnInteractionResume;

		public InteractionDelegate OnInteractionStop;

		public InteractionEventDelegate OnInteractionEvent;

		public RaycastHit raycastHit;

		[Space]
		[SerializeField]
		private FullBodyBipedIK fullBody;

		public InteractionLookAt lookAt;

		private InteractionEffector[] interactionEffectors;

		private bool initiated;

		private Collider lastCollider;

		private Collider c;

		public bool inInteraction => false;

		public FullBodyBipedIK ik
		{
			get
			{
				return null;
			}
			set
			{
			}
		}

		public List<InteractionTrigger> triggersInRange { get; private set; }

		private void OpenUserManual()
		{
		}

		private void OpenScriptReference()
		{
		}

		private void OpenTutorial1()
		{
		}

		private void OpenTutorial2()
		{
		}

		private void OpenTutorial3()
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

		public bool IsInInteraction(FullBodyBipedEffector effectorType)
		{
			return false;
		}

		public bool IsPaused(FullBodyBipedEffector effectorType)
		{
			return false;
		}

		public bool IsPaused()
		{
			return false;
		}

		public bool IsInSync()
		{
			return false;
		}

		public bool StartInteraction(FullBodyBipedEffector effectorType, InteractionObject interactionObject, bool interrupt)
		{
			return false;
		}

		public bool PauseInteraction(FullBodyBipedEffector effectorType)
		{
			return false;
		}

		public bool ResumeInteraction(FullBodyBipedEffector effectorType)
		{
			return false;
		}

		public bool StopInteraction(FullBodyBipedEffector effectorType)
		{
			return false;
		}

		public void PauseAll()
		{
		}

		public void ResumeAll()
		{
		}

		public void StopAll()
		{
		}

		public InteractionObject GetInteractionObject(FullBodyBipedEffector effectorType)
		{
			return null;
		}

		public float GetProgress(FullBodyBipedEffector effectorType)
		{
			return 0f;
		}

		public float GetMinActiveProgress()
		{
			return 0f;
		}

		public bool TriggerInteraction(int index, bool interrupt)
		{
			return false;
		}

		public bool TriggerInteraction(int index, bool interrupt, out InteractionObject interactionObject)
		{
			interactionObject = null;
			return false;
		}

		public bool TriggerInteraction(int index, bool interrupt, out InteractionTarget interactionTarget)
		{
			interactionTarget = null;
			return false;
		}

		public InteractionTrigger.Range GetClosestInteractionRange()
		{
			return null;
		}

		public InteractionObject GetClosestInteractionObjectInRange()
		{
			return null;
		}

		public InteractionTarget GetClosestInteractionTargetInRange()
		{
			return null;
		}

		public InteractionObject[] GetClosestInteractionObjectsInRange()
		{
			return null;
		}

		public InteractionTarget[] GetClosestInteractionTargetsInRange()
		{
			return null;
		}

		public bool TriggerEffectorsReady(int index)
		{
			return false;
		}

		public InteractionTrigger.Range GetTriggerRange(int index)
		{
			return null;
		}

		public int GetClosestTriggerIndex()
		{
			return 0;
		}

		public void Start()
		{
		}

		private void InteractionPause(FullBodyBipedEffector effector, InteractionObject interactionObject)
		{
		}

		private void InteractionResume(FullBodyBipedEffector effector, InteractionObject interactionObject)
		{
		}

		private void InteractionStop(FullBodyBipedEffector effector, InteractionObject interactionObject)
		{
		}

		private void LookAtInteraction(FullBodyBipedEffector effector, InteractionObject interactionObject)
		{
		}

		public void OnTriggerEnter(Collider c)
		{
		}

		public void OnTriggerExit(Collider c)
		{
		}

		private bool ContactIsInRange(int index, out int bestRangeIndex)
		{
			bestRangeIndex = default;
			return false;
		}

		private void OnDrawGizmosSelected()
		{
		}

		public void Update()
		{
		}

		private void Raycasting()
		{
		}

		private void UpdateTriggerEventBroadcasting()
		{
		}

		private void UpdateEffectors()
		{
		}

		private void OnPreFBBIK()
		{
		}

		private void OnPostFBBIK()
		{
		}

		private void OnFixTransforms()
		{
		}

		private void OnDestroy()
		{
		}

		private bool IsValid(bool log)
		{
			return false;
		}

		private bool TriggerIndexIsValid(int index)
		{
			return false;
		}
	}
}
