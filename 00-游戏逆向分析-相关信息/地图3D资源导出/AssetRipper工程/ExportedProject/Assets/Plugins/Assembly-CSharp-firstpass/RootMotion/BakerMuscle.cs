using System;
using UnityEngine;

namespace RootMotion
{
	[Serializable]
	public class BakerMuscle
	{
		public AnimationCurve curve;

		private int muscleIndex;

		private string propertyName;

		public BakerMuscle(int muscleIndex)
		{
		}

		private string MuscleNameToPropertyName(string n)
		{
			return null;
		}

		public void MultiplyLength(AnimationCurve curve, float mlp)
		{
		}

		public void SetCurves(ref AnimationClip clip, float maxError, float lengthMlp)
		{
		}

		public void Reset()
		{
		}

		public void SetKeyframe(float time, float[] muscles)
		{
		}

		public void SetLoopFrame(float time)
		{
		}
	}
}
