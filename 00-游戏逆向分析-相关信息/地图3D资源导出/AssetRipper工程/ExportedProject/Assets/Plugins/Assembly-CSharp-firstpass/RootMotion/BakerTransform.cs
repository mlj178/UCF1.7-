using System;
using UnityEngine;

namespace RootMotion
{
	[Serializable]
	public class BakerTransform
	{
		public Transform transform;

		public AnimationCurve posX;

		public AnimationCurve posY;

		public AnimationCurve posZ;

		public AnimationCurve rotX;

		public AnimationCurve rotY;

		public AnimationCurve rotZ;

		public AnimationCurve rotW;

		private string relativePath;

		private bool recordPosition;

		private Vector3 relativePosition;

		private bool isRootNode;

		private Quaternion relativeRotation;

		public BakerTransform(Transform transform, Transform root, bool recordPosition, bool isRootNode)
		{
		}

		public void SetRelativeSpace(Vector3 position, Quaternion rotation)
		{
		}

		public void SetCurves(ref AnimationClip clip)
		{
		}

		private void AddRootMotionCurves(ref AnimationClip clip)
		{
		}

		public void Reset()
		{
		}

		public void ReduceKeyframes(float maxError)
		{
		}

		public void SetKeyframes(float time)
		{
		}

		public void AddLoopFrame(float time)
		{
		}
	}
}
