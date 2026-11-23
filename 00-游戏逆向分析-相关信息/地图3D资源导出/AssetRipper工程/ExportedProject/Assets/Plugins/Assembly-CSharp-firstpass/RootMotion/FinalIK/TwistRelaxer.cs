using UnityEngine;

namespace RootMotion.FinalIK
{
	public class TwistRelaxer : MonoBehaviour
	{
		public IK ik;

		public Transform parent;

		public Transform child;

		public float weight;

		public float parentChildCrossfade;

		public float twistAngleOffset;

		private Vector3 twistAxis;

		private Vector3 axis;

		private Vector3 axisRelativeToParentDefault;

		private Vector3 axisRelativeToChildDefault;

		public void Relax()
		{
		}

		private void Start()
		{
		}

		private void OnPostUpdate()
		{
		}

		private void LateUpdate()
		{
		}

		private void OnDestroy()
		{
		}
	}
}
