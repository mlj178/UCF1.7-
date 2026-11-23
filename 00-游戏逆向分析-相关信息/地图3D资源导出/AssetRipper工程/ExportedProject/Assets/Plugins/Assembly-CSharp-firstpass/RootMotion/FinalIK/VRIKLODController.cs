using UnityEngine;

namespace RootMotion.FinalIK
{
	public class VRIKLODController : MonoBehaviour
	{
		public Renderer LODRenderer;

		public float LODDistance;

		public bool allowCulled;

		private VRIK ik;

		private void Start()
		{
		}

		private void Update()
		{
		}

		private int GetLODLevel()
		{
			return 0;
		}
	}
}
