using System;
using UnityEngine;
using UnityEngine.Events;

namespace RootMotion.FinalIK
{
	public class InteractionObject : MonoBehaviour
	{
		[Serializable]
		public class InteractionEvent
		{
			public float time;

			public bool pause;

			public bool pickUp;

			public AnimatorEvent[] animations;

			public Message[] messages;

			public UnityEvent unityEvent;

			public void Activate(Transform t)
			{
			}
		}

		[Serializable]
		public class Message
		{
			public string function;

			public GameObject recipient;

			private const string empty = "";

			public void Send(Transform t)
			{
			}
		}

		[Serializable]
		public class AnimatorEvent
		{
			public Animator animator;

			public Animation animation;

			public string animationState;

			public float crossfadeTime;

			public int layer;

			public bool resetNormalizedTime;

			private const string empty = "";

			public void Activate(bool pickUp)
			{
			}

			private void Activate(Animator animator)
			{
			}

			private void Activate(Animation animation)
			{
			}
		}

		[Serializable]
		public class WeightCurve
		{
			[Serializable]
			public enum Type
			{
				PositionWeight = 0,
				RotationWeight = 1,
				PositionOffsetX = 2,
				PositionOffsetY = 3,
				PositionOffsetZ = 4,
				Pull = 5,
				Reach = 6,
				RotateBoneWeight = 7,
				Push = 8,
				PushParent = 9,
				PoserWeight = 10,
				BendGoalWeight = 11
			}

			public Type type;

			public AnimationCurve curve;

			public float GetValue(float timer)
			{
				return 0f;
			}
		}

		[Serializable]
		public class Multiplier
		{
			public WeightCurve.Type curve;

			public float multiplier;

			public WeightCurve.Type result;

			public float GetValue(WeightCurve weightCurve, float timer)
			{
				return 0f;
			}
		}

		public Transform otherLookAtTarget;

		public Transform otherTargetsRoot;

		public Transform positionOffsetSpace;

		public WeightCurve[] weightCurves;

		public Multiplier[] multipliers;

		public InteractionEvent[] events;

		private InteractionTarget[] targets;

		public float length { get; private set; }

		public InteractionSystem lastUsedInteractionSystem { get; private set; }

		public Transform lookAtTarget => null;

		public Transform targetsRoot => null;

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

		public void Initiate()
		{
		}

		public InteractionTarget GetTarget(FullBodyBipedEffector effectorType, InteractionSystem interactionSystem)
		{
			return null;
		}

		public bool CurveUsed(WeightCurve.Type type)
		{
			return false;
		}

		public InteractionTarget[] GetTargets()
		{
			return null;
		}

		public Transform GetTarget(FullBodyBipedEffector effectorType, string tag)
		{
			return null;
		}

		public void OnStartInteraction(InteractionSystem interactionSystem)
		{
		}

		public void Apply(IKSolverFullBodyBiped solver, FullBodyBipedEffector effector, InteractionTarget target, float timer, float weight)
		{
		}

		public float GetValue(WeightCurve.Type weightCurveType, InteractionTarget target, float timer)
		{
			return 0f;
		}

		private void Start()
		{
		}

		private void Apply(IKSolverFullBodyBiped solver, FullBodyBipedEffector effector, WeightCurve.Type type, float value, float weight)
		{
		}

		private Transform GetTarget(FullBodyBipedEffector effectorType)
		{
			return null;
		}

		private int GetWeightCurveIndex(WeightCurve.Type weightCurveType)
		{
			return 0;
		}

		private int GetMultiplierIndex(WeightCurve.Type weightCurveType)
		{
			return 0;
		}
	}
}
