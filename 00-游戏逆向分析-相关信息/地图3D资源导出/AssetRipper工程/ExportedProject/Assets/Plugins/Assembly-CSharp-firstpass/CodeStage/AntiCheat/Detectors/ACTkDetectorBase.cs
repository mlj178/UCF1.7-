using System;
using System.Runtime.CompilerServices;
using UnityEngine;
using UnityEngine.Events;

namespace CodeStage.AntiCheat.Detectors
{
	public abstract class ACTkDetectorBase : MonoBehaviour
	{
		protected const string ContainerName = "Anti-Cheat Toolkit Detectors";

		protected const string MenuPath = "Code Stage/Anti-Cheat Toolkit/";

		protected const string GameObjectMenuPath = "GameObject/Create Other/Code Stage/Anti-Cheat Toolkit/";

		protected static GameObject detectorsContainer;

		public bool autoStart;

		public bool keepAlive;

		public bool autoDispose;

		[CompilerGenerated]
		private Action m_CheatDetected;

		[SerializeField]
		protected UnityEvent detectionEvent;

		[SerializeField]
		protected bool detectionEventHasListener;

		protected bool started;

		protected bool isRunning;

		public bool IsRunning => false;

		public event Action CheatDetected
		{
			[CompilerGenerated]
			add
			{
			}
			[CompilerGenerated]
			remove
			{
			}
		}

		private void Start()
		{
		}

		private void OnEnable()
		{
		}

		private void OnDisable()
		{
		}

		private void OnApplicationQuit()
		{
		}

		protected virtual void OnDestroy()
		{
		}

		internal virtual void OnCheatingDetected()
		{
		}

		protected virtual bool Init(ACTkDetectorBase instance, string detectorName)
		{
			return false;
		}

		protected virtual void DisposeInternal()
		{
		}

		protected virtual bool DetectorHasCallbacks()
		{
			return false;
		}

		protected virtual void StopDetectionInternal()
		{
		}

		protected virtual void PauseDetector()
		{
		}

		protected virtual bool ResumeDetector()
		{
			return false;
		}

		protected abstract void StartDetectionAutomatically();
	}
}
