using System;
using UnityEngine;

namespace RootMotion.FinalIK
{
	public class HitReaction : OffsetModifier
	{
		[Serializable]
		public abstract class HitPoint
		{
			public string name;

			public Collider collider;

			[SerializeField]
			private float crossFadeTime;

			private float length;

			private float crossFadeSpeed;

			private float lastTime;

			public bool inProgress => false;

			protected float crossFader { get; private set; }

			protected float timer { get; private set; }

			protected Vector3 force { get; private set; }

			protected Vector3 point { get; private set; }

			public void Hit(Vector3 force, Vector3 point)
			{
			}

			public void Apply(IKSolverFullBodyBiped solver, float weight)
			{
			}

			protected abstract float GetLength();

			protected abstract void CrossFadeStart();

			protected abstract void OnApply(IKSolverFullBodyBiped solver, float weight);
		}

		[Serializable]
		public class HitPointEffector : HitPoint
		{
			[Serializable]
			public class EffectorLink
			{
				public FullBodyBipedEffector effector;

				public float weight;

				private Vector3 lastValue;

				private Vector3 current;

				public void Apply(IKSolverFullBodyBiped solver, Vector3 offset, float crossFader)
				{
				}

				public void CrossFadeStart()
				{
				}
			}

			public AnimationCurve offsetInForceDirection;

			public AnimationCurve offsetInUpDirection;

			public EffectorLink[] effectorLinks;

			protected override float GetLength()
			{
				return 0f;
			}

			protected override void CrossFadeStart()
			{
			}

			protected override void OnApply(IKSolverFullBodyBiped solver, float weight)
			{
			}
		}

		[Serializable]
		public class HitPointBone : HitPoint
		{
			[Serializable]
			public class BoneLink
			{
				public Transform bone;

				public float weight;

				private Quaternion lastValue;

				private Quaternion current;

				public void Apply(IKSolverFullBodyBiped solver, Quaternion offset, float crossFader)
				{
				}

				public void CrossFadeStart()
				{
				}
			}

			public AnimationCurve aroundCenterOfMass;

			public BoneLink[] boneLinks;

			private Rigidbody rigidbody;

			protected override float GetLength()
			{
				return 0f;
			}

			protected override void CrossFadeStart()
			{
			}

			protected override void OnApply(IKSolverFullBodyBiped solver, float weight)
			{
			}
		}

		public HitPointEffector[] effectorHitPoints;

		public HitPointBone[] boneHitPoints;

		public bool inProgress => false;

		protected override void OnModifyOffset()
		{
		}

		public void Hit(Collider collider, Vector3 force, Vector3 point)
		{
		}
	}
}
