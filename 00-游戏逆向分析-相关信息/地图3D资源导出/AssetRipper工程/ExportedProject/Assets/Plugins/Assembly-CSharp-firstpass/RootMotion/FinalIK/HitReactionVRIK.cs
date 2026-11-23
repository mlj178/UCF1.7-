using System;
using UnityEngine;

namespace RootMotion.FinalIK
{
	public class HitReactionVRIK : OffsetModifierVRIK
	{
		[Serializable]
		public abstract class Offset
		{
			public string name;

			public Collider collider;

			[SerializeField]
			private float crossFadeTime;

			private float length;

			private float crossFadeSpeed;

			private float lastTime;

			protected float crossFader { get; private set; }

			protected float timer { get; private set; }

			protected Vector3 force { get; private set; }

			protected Vector3 point { get; private set; }

			public void Hit(Vector3 force, AnimationCurve[] curves, Vector3 point)
			{
			}

			public void Apply(VRIK ik, AnimationCurve[] curves, float weight)
			{
			}

			protected abstract float GetLength(AnimationCurve[] curves);

			protected abstract void CrossFadeStart();

			protected abstract void OnApply(VRIK ik, AnimationCurve[] curves, float weight);
		}

		[Serializable]
		public class PositionOffset : Offset
		{
			[Serializable]
			public class PositionOffsetLink
			{
				public IKSolverVR.PositionOffset positionOffset;

				public float weight;

				private Vector3 lastValue;

				private Vector3 current;

				public void Apply(VRIK ik, Vector3 offset, float crossFader)
				{
				}

				public void CrossFadeStart()
				{
				}
			}

			public int forceDirCurveIndex;

			public int upDirCurveIndex;

			public PositionOffsetLink[] offsetLinks;

			protected override float GetLength(AnimationCurve[] curves)
			{
				return 0f;
			}

			protected override void CrossFadeStart()
			{
			}

			protected override void OnApply(VRIK ik, AnimationCurve[] curves, float weight)
			{
			}
		}

		[Serializable]
		public class RotationOffset : Offset
		{
			[Serializable]
			public class RotationOffsetLink
			{
				public IKSolverVR.RotationOffset rotationOffset;

				public float weight;

				private Quaternion lastValue;

				private Quaternion current;

				public void Apply(VRIK ik, Quaternion offset, float crossFader)
				{
				}

				public void CrossFadeStart()
				{
				}
			}

			public int curveIndex;

			public RotationOffsetLink[] offsetLinks;

			private Rigidbody rigidbody;

			protected override float GetLength(AnimationCurve[] curves)
			{
				return 0f;
			}

			protected override void CrossFadeStart()
			{
			}

			protected override void OnApply(VRIK ik, AnimationCurve[] curves, float weight)
			{
			}
		}

		public AnimationCurve[] offsetCurves;

		public PositionOffset[] positionOffsets;

		public RotationOffset[] rotationOffsets;

		protected override void OnModifyOffset()
		{
		}

		public void Hit(Collider collider, Vector3 force, Vector3 point)
		{
		}
	}
}
