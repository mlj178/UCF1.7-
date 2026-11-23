using System;
using UnityEngine;
using UnityEngine.Playables;

namespace RootMotion
{
	public abstract class Baker : MonoBehaviour
	{
		[Serializable]
		public enum Mode
		{
			AnimationClips = 0,
			AnimationStates = 1,
			PlayableDirector = 2,
			Realtime = 3
		}

		public int frameRate;

		public float keyReductionError;

		public Mode mode;

		public AnimationClip[] animationClips;

		public string[] animationStates;

		public bool loop;

		public string saveToFolder;

		public string appendName;

		public string saveName;

		[HideInInspector]
		[SerializeField]
		public Animator animator;

		[HideInInspector]
		[SerializeField]
		public PlayableDirector director;

		public bool isBaking { get; private set; }

		public float bakingProgress { get; private set; }

		protected float clipLength { get; private set; }

		private void OpenUserManual()
		{
		}

		private void OpenScriptReference()
		{
		}

		private void SupportGroup()
		{
		}

		private void ASThread()
		{
		}

		protected abstract Transform GetCharacterRoot();

		protected abstract void OnStartBaking();

		protected abstract void OnSetLoopFrame(float time);

		protected abstract void OnSetCurves(ref AnimationClip clip);

		protected abstract void OnSetKeyframes(float time, bool lastFrame);

		public void BakeClip()
		{
		}

		public void StartBaking()
		{
		}

		public void StopBaking()
		{
		}
	}
}
