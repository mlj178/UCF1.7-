using UnityEngine;

namespace RootMotion
{
	public class SolverManager : MonoBehaviour
	{
		public bool fixTransforms;

		private Animator animator;

		private Animation legacy;

		private bool updateFrame;

		private bool componentInitiated;

		private bool skipSolverUpdate;

		private bool animatePhysics => false;

		private bool isAnimated => false;

		public void Disable()
		{
		}

		protected virtual void InitiateSolver()
		{
		}

		protected virtual void UpdateSolver()
		{
		}

		protected virtual void FixTransforms()
		{
		}

		private void OnDisable()
		{
		}

		private void Start()
		{
		}

		private void Initiate()
		{
		}

		private void Update()
		{
		}

		private void FindAnimatorRecursive(Transform t, bool findInChildren)
		{
		}

		private void FixedUpdate()
		{
		}

		private void LateUpdate()
		{
		}

		public void UpdateSolverExternal()
		{
		}
	}
}
