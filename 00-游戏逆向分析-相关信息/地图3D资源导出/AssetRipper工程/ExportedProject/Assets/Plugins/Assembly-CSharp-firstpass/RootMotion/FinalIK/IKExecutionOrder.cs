using UnityEngine;

namespace RootMotion.FinalIK
{
	public class IKExecutionOrder : MonoBehaviour
	{
		public IK[] IKComponents;

		public Animator animator;

		private bool fixedFrame;

		private bool animatePhysics => false;

		private void Start()
		{
		}

		private void Update()
		{
		}

		private void FixedUpdate()
		{
		}

		private void LateUpdate()
		{
		}

		private void FixTransforms()
		{
		}
	}
}
