using System;

namespace WeaponNS.Component
{
	[Serializable]
	public class RepeatFireData : ComponentDataBase
	{
		public bool triggerMode;

		public float coldTime;

		public float shootInterval;
	}
}
