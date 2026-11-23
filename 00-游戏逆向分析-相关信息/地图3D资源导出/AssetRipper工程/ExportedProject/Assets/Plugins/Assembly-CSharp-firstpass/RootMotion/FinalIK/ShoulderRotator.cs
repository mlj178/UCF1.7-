using UnityEngine;

namespace RootMotion.FinalIK
{
	public class ShoulderRotator : MonoBehaviour
	{
		public float weight;

		public float offset;

		private FullBodyBipedIK ik;

		private bool skip;

		private void Start()
		{
		}

		private void RotateShoulders()
		{
		}

		private void RotateShoulder(FullBodyBipedChain chain, float weight, float offset)
		{
		}

		private IKMapping.BoneMap GetParentBoneMap(FullBodyBipedChain chain)
		{
			return null;
		}

		private void OnDestroy()
		{
		}
	}
}
