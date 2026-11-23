using System;
using System.Collections;
using UnityEngine;

namespace RootMotion.FinalIK
{
	public abstract class OffsetModifier : MonoBehaviour
	{
		[Serializable]
		public class OffsetLimits
		{
			public FullBodyBipedEffector effector;

			public float spring;

			public bool x;

			public bool y;

			public bool z;

			public float minX;

			public float maxX;

			public float minY;

			public float maxY;

			public float minZ;

			public float maxZ;

			public void Apply(IKEffector e, Quaternion rootRotation)
			{
			}

			private float SpringAxis(float value, float min, float max)
			{
				return 0f;
			}

			private float Spring(float value, float limit, bool negative)
			{
				return 0f;
			}
		}

		public float weight;

		public FullBodyBipedIK ik;

		protected float lastTime;

		protected float deltaTime => 0f;

		protected abstract void OnModifyOffset();

		protected virtual void Start()
		{
		}

		private IEnumerator Initiate()
		{
			return null;
		}

		private void ModifyOffset()
		{
		}

		protected void ApplyLimits(OffsetLimits[] limits)
		{
		}

		protected virtual void OnDestroy()
		{
		}
	}
}
