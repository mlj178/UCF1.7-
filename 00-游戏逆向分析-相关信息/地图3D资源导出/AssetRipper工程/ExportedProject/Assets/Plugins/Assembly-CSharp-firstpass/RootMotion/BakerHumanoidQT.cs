using System;
using UnityEngine;

namespace RootMotion
{
	[Serializable]
	public class BakerHumanoidQT
	{
		private Transform transform;

		private string Qx;

		private string Qy;

		private string Qz;

		private string Qw;

		private string Tx;

		private string Ty;

		private string Tz;

		public AnimationCurve rotX;

		public AnimationCurve rotY;

		public AnimationCurve rotZ;

		public AnimationCurve rotW;

		public AnimationCurve posX;

		public AnimationCurve posY;

		public AnimationCurve posZ;

		private AvatarIKGoal goal;

		private Quaternion lastQ;

		private bool lastQSet;

		public BakerHumanoidQT(string name)
		{
		}

		public BakerHumanoidQT(Transform transform, AvatarIKGoal goal, string name)
		{
		}

		public void Reset()
		{
		}

		public void SetIKKeyframes(float time, Avatar avatar, float humanScale, Vector3 bodyPosition, Quaternion bodyRotation)
		{
		}

		public void SetKeyframes(float time, Vector3 pos, Quaternion rot)
		{
		}

		public void MoveLastKeyframes(float time)
		{
		}

		public void SetLoopFrame(float time)
		{
		}

		private void MoveLastKeyframe(float time, AnimationCurve curve)
		{
		}

		public void MultiplyLength(AnimationCurve curve, float mlp)
		{
		}

		public void SetCurves(ref AnimationClip clip, float maxError, float lengthMlp)
		{
		}
	}
}
