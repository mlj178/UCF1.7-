using System.Collections;
using UnityEngine;

namespace RootMotion.FinalIK
{
	public abstract class OffsetModifierVRIK : MonoBehaviour
	{
		public float weight;

		public VRIK ik;

		private float lastTime;

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

		protected virtual void OnDestroy()
		{
		}
	}
}
