using System.Collections;
using UnityEngine;

namespace RootMotion.FinalIK
{
	public class RagdollUtility : MonoBehaviour
	{
		public class Rigidbone
		{
			public Rigidbody r;

			public Transform t;

			public Collider collider;

			public Joint joint;

			public Rigidbody c;

			public bool updateAnchor;

			public Vector3 deltaPosition;

			public Quaternion deltaRotation;

			public float deltaTime;

			public Vector3 lastPosition;

			public Quaternion lastRotation;

			public Rigidbone(Rigidbody r)
			{
			}

			public void RecordVelocity()
			{
			}

			public void WakeUp(float velocityWeight, float angularVelocityWeight)
			{
			}
		}

		public class Child
		{
			public Transform t;

			public Vector3 localPosition;

			public Quaternion localRotation;

			public Child(Transform transform)
			{
			}

			public void FixTransform(float weight)
			{
			}

			public void StoreLocalState()
			{
			}
		}

		public IK ik;

		public float ragdollToAnimationTime;

		public bool applyIkOnRagdoll;

		public float applyVelocity;

		public float applyAngularVelocity;

		private Animator animator;

		private Rigidbone[] rigidbones;

		private Child[] children;

		private bool enableRagdollFlag;

		private AnimatorUpdateMode animatorUpdateMode;

		private IK[] allIKComponents;

		private bool[] fixTransforms;

		private float ragdollWeight;

		private float ragdollWeightV;

		private bool fixedFrame;

		private bool[] disabledIKComponents;

		private bool isRagdoll => false;

		private bool ikUsed => false;

		public void EnableRagdoll()
		{
		}

		public void DisableRagdoll()
		{
		}

		public void Start()
		{
		}

		private IEnumerator DisableRagdollSmooth()
		{
			return null;
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

		private void AfterLastIK()
		{
		}

		private void AfterAnimation()
		{
		}

		private void OnFinalPose()
		{
		}

		private void RagdollEnabler()
		{
		}

		private void RecordVelocities()
		{
		}

		private void StoreLocalState()
		{
		}

		private void FixTransforms(float weight)
		{
		}

		private void OnDestroy()
		{
		}
	}
}
