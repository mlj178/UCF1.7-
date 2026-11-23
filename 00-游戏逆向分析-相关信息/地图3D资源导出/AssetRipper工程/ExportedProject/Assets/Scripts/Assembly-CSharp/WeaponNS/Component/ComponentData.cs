using System;
using System.Collections.Generic;
using UnityEngine;

namespace WeaponNS.Component
{
	[Serializable]
	public class ComponentData
	{
		[SerializeReference]
		public List<ComponentDataBase> list;

		public void AddComponent_Float()
		{
		}

		public void AddComponent_RepeatFire()
		{
		}

		public T Get<T>() where T : ComponentDataBase
		{
			return null;
		}
	}
}
