using System;
using UnityEngine;

namespace RootMotion.Demos
{
	public class FKOffset : MonoBehaviour
	{
		[Serializable]
		public class Offset
		{
			[SerializeField]
			[HideInInspector]
			public string name;

			public HumanBodyBones bone;

			public Vector3 rotationOffset;

			private Transform t;

			public void Apply(Animator animator)
			{
			}
		}

		public Offset[] offsets;

		private Animator animator;

		private void Start()
		{
		}

		private void LateUpdate()
		{
		}

		private void OnDrawGizmosSelected()
		{
		}
	}
}
