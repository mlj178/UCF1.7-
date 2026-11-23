using UnityEngine;

namespace RootMotion
{
	public class GenericBaker : Baker
	{
		public bool markAsLegacy;

		public Transform root;

		public Transform rootNode;

		public Transform[] ignoreList;

		public Transform[] bakePositionList;

		private BakerTransform[] children;

		private BakerTransform rootChild;

		private int rootChildIndex;

		private void Awake()
		{
		}

		protected override Transform GetCharacterRoot()
		{
			return null;
		}

		protected override void OnStartBaking()
		{
		}

		protected override void OnSetLoopFrame(float time)
		{
		}

		protected override void OnSetCurves(ref AnimationClip clip)
		{
		}

		protected override void OnSetKeyframes(float time, bool lastFrame)
		{
		}

		private bool IsIgnored(Transform t)
		{
			return false;
		}

		private bool BakePosition(Transform t)
		{
			return false;
		}
	}
}
